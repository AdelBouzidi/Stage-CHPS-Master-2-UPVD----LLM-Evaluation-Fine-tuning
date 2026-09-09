program main
  implicit none
  integer :: n
  integer, allocatable :: result(:)
  
  ! Read input
  read *, n
  
  ! Call the function
  result = get_odd_collatz(n)
  
  ! Print output
  print *, result
contains

  function get_odd_collatz(n) result(res)
    implicit none
    integer, intent(in) :: n
    integer, allocatable :: res(:)
    integer :: i, temp
    integer :: count
    
    ! Initialize result array
    count = 0
    temp = n
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
    if (mod(n, 2) /= 0) then
      count = count + 1
    end if
    if (mod(temp, 2) /= 0) then
      count = count + 1
    end if
    
    allocate(res(count))
    i = 1
    temp = n
    do while (temp /= 1)
      if (mod(temp, 2) /= 0) then
        res(i) = temp
        i = i + 1
      end if
      if (mod(temp, 2) == 0) then
        temp = temp / 2
      else
        temp = 3 * temp + 1
      end if
    end do
    if (mod(n, 2) /= 0) then
      res(i) = n
      i = i + 1
    end if
    if (mod(temp, 2) /= 0) then
      res(i) = temp
    end if
  end function get_odd_collatz

end program main