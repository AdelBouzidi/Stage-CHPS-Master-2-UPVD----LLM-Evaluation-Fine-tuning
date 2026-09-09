program get_odd_collatz_demo
  implicit none
  integer, parameter :: dp = kind(1.0d0)
  integer :: n
  integer, allocatable :: result(:)
  integer :: i, size

  ! Hardcoded input value (example: 5)
  n = 5

  ! Call the function
  call get_odd_collatz(n, result, size)

  ! Print the result
  print *, 'Result:', (result(i), i=1,size)

contains

  subroutine get_odd_collatz(n, result, size)
    implicit none
    integer, intent(in) :: n
    integer, intent(out) :: result(:)
    integer, intent(out) :: size
    integer :: i, temp, count

    temp = n
    count = 0
    do while (temp /= 1)
      if (mod(temp, 2) /= 0) then
        count = count + 1
      end if
      if (mod(temp, 2) == 0) then
        temp = temp / 2
      else
        temp = 3 * temp + 1
      end if
    end do
    if (mod(n, 2) /= 0) count = count + 1

    allocate(result(count))
    result = 0
    i = 0
    do while (temp /= 1)
      i = i + 1
      if (mod(temp, 2) /= 0) then
        result(i) = temp
      end if
      if (mod(temp, 2) == 0) then
        temp = temp / 2
      else
        temp = 3 * temp + 1
      end if
    end do
    i = i + 1
    result(i) = temp

    size = count
  end subroutine get_odd_collatz

end program get_odd_collatz_demo