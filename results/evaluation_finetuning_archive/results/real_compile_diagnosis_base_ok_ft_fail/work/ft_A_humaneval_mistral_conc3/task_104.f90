program main
  implicit none
  integer :: x_len
  integer, allocatable :: x(:)
  integer, allocatable :: result(:)
  integer :: i, j, k, n, len
  integer :: temp
  character(len=1) :: c
  logical :: has_even

  ! Hardcoded input as per example
  x_len = 4
  allocate(x(x_len))
  x = [15, 33, 1422, 1]

  ! Call the function
  result = unique_digits(x_len, x)

  ! Output the result
  print *, result

contains

  function unique_digits(x_len, x) result(res)
    implicit none
    integer, intent(in) :: x_len
    integer, intent(in) :: x(x_len)
    integer, allocatable :: res(:)
    integer :: i, j, k, n, len
    integer :: temp
    character(len=1) :: c
    logical :: has_even

    ! Initialize result array
    allocate(res(x_len))
    n = 0
    do i = 1, x_len
      has_even = .false.
      len = len(str(x(i)))
      do j = 1, len
        c = achar(iachar(achar(j:j)))
        if (mod(iachar(c), 2) == 0) then
          has_even = .true.
          exit
        end if
      end do
      if (.not. has_even) then
        n = n + 1
        res(n) = x(i)
      end if
    end do
    ! Sort the result
    do i = 1, n-1
      do j = i+1, n
        if (res(i) > res(j)) then
          temp = res(i)
          res(i) = res(j)
          res(j) = temp
        end if
      end do
    end do
  end function unique_digits

end program main