program factorize_demo
  implicit none
  integer, dimension(:), allocatable :: factors
  integer :: n

  ! Read input
  read(*,*) n

  ! Call factorize function
  factors = factorize(n)

  ! Print output
  print *, factors

contains

  function factorize(n) result(factors)
    implicit none
    integer, intent(in) :: n
    integer, dimension(:), allocatable :: factors
    integer :: i, count
    integer, dimension(100) :: temp_factors

    if (n <= 1) then
      allocate(factors(0))
      return
    end if

    allocate(factors(100))
    count = 0
    do i = 2, n
      if (mod(n, i) == 0) then
        count = count + 1
        factors(count) = i
        n = n / i
      else
        if (n == 1) exit
      end if
    end do

    allocate(factors(count))
  end function factorize

end program factorize_demo