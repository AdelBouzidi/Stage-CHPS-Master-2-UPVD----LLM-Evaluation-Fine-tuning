program main
  implicit none
  integer :: n
  integer, allocatable :: result(:)
  
  ! Read input
  read(*,*) n
  
  ! Call the function
  result = get_odd_collatz(n)
  
  ! Print output
  write(*,*) result
contains
  function get_odd_collatz(n) result(res)
    implicit none
    integer, intent(in) :: n
    integer, allocatable :: res(:)
    integer :: i, temp
    integer :: count
    
    ! Count odd numbers in the sequence
    temp = n
    count = 0
    do while (temp > 0)
      if (mod(temp, 2) == 1) then
        count = count + 1
      end if
      if (temp == 1) exit
      if (mod(temp, 2) == 0) then
        temp = temp / 2
      else
        temp = 3 * temp + 1
      end if
    end do
    
    ! Allocate result array
    allocate(res(count))
    
    ! Fill result array with odd numbers
    temp = n
    i = 1
    do while (temp > 0)
      if (mod(temp, 2) == 1) then
        res(i) = temp
        i = i + 1
      end if
      if (temp == 1) exit
      if (mod(temp, 2) == 0) then
        temp = temp / 2
      else
        temp = 3 * temp + 1
      end if
    end do
  end function get_odd_collatz
end program main