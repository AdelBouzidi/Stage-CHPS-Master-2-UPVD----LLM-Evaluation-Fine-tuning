program factorize_demo
  implicit none
  integer :: n
  integer, allocatable :: factors(:)
  integer :: i

  ! Read input number
  read(*,*) n

  ! Call the factorize function
  call factorize(n, factors)

  ! Output the factors
  print *, factors

contains

  subroutine factorize(n, factors)
    implicit none
    integer, intent(in) :: n
    integer, intent(out), allocatable :: factors(:)
    integer :: i, j, count
    integer :: temp

    ! Handle edge cases
    if (n <= 1) then
      allocate(factors(0))
      return
    end if

    ! Count factors
    count = 0
    temp = n
    do i = 2, n
      if (mod(temp, i) == 0) then
        count = count + 1
        temp = temp / i
      else
        exit
      end if
    end do

    ! Allocate array
    allocate(factors(count))

    ! Fill array with factors
    i = 1
    temp = n
    do j = 2, n
      if (mod(temp, j) == 0) then
        factors(i) = j
        i = i + 1
        temp = temp / j
      else
        exit
      end if
    end do

  end subroutine factorize

end program factorize_demo